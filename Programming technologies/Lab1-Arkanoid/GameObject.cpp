#include "GameObject.h"

#include "MathHelper.h"
#include "NearlyEqual.h"

#include <algorithm>
#include <stdexcept>

#include <tuple>

namespace arkanoid {

    GameObject::GameObject(Point topLeft,
                           double maxPositioX, double maxPositionY,
                           double width, double height,
                           double velocity, double angle)
            :mTopLeft{ topLeft },
             mMaxPositionX(maxPositioX),
             mMaxPositionY(maxPositionY),
             mWidth{ width },
             mHeight{ height },
             mVelocity{ velocity },
             mQuadrant{ calcQuadrant(angle) },
             mQuadrantAngle{ angleToQuadrantAngle(angle, mQuadrant) }
    {
    }

    GameObject::~GameObject() = default;

    Point GameObject::topLeft() const
    {
        return mTopLeft;
    }

    void GameObject::setTopLeft(Point topLeft)
    {
        mTopLeft = topLeft;
    }

    Point GameObject::bottomRight() const
    {
        return Point{ mTopLeft.x + mWidth , mTopLeft.y + mHeight };
    }

    double GameObject::velocity() const
    {
        return mVelocity;
    }

    void GameObject::setVelocity(double velocity)
    {
        mVelocity = velocity;
    }

    double GameObject::angle() const
    {
        return qudrantAngleToAngle(mQuadrantAngle, mQuadrant);
    }

    void GameObject::setAngle(double angle)
    {
        angle = calcAlphaIfOver360(angle);
        mQuadrant = calcQuadrant(angle);
        mQuadrantAngle = angleToQuadrantAngle(angle, mQuadrant);
    }

    double GameObject::quadrantAngle() const
    {
        return mQuadrantAngle;
    }

    Quadrant GameObject::quadrant() const
    {
        return mQuadrant;
    }

    double GameObject::width() const
    {
        return mWidth;
    }

    double GameObject::height() const
    {
        return mHeight;
    }

    void GameObject::move(double elapsedTimeInMS)
    {
        auto distance = calcTraveldWay(elapsedTimeInMS, mVelocity);
        auto traveldWay = calcDelta(mQuadrantAngle, mQuadrant, distance);

        mTopLeft.x += traveldWay.x;
        mTopLeft.y += traveldWay.y;

        auto maxX = mTopLeft.x + mWidth;
        mTopLeft.x = std::clamp(maxX, mWidth, mMaxPositionX) - mWidth;

        auto maxY = mTopLeft.y + mHeight;
        mTopLeft.y = std::clamp(maxY, mHeight, mMaxPositionY) - mHeight;
    }

    bool GameObject::reflectIfHit(const GameObject& obj)
    {
        auto oldQuadrant = mQuadrant;

        switch (mQuadrant)
        {
            case Quadrant::I:
                reflectFromQuadrantOneIfHit(obj);
                break;
            case Quadrant::II:
                reflectFromQuadrantTwoIfHit(obj);
                break;
            case Quadrant::III:
                reflectFromQuadrantThreeIfHit(obj);
                break;
            case Quadrant::IV:
                reflectFromQuadrantFourIfHit(obj);
                break;
        }

        return mQuadrant != oldQuadrant;
    }

    void GameObject::reflectFromQuadrantOneIfHit(const GameObject& obj)
    {
        if (interectsWithBottomY(*this, obj)) {
            reflectToQuadrantFourIfIntersectsWithX(obj);
        }
        else if (interectsWithRightX(*this, obj)) {
            reflectToQuadrantTwoIfIntersectsWithY(obj);
        }
    }

    void GameObject::reflectFromQuadrantTwoIfHit(const GameObject& obj)
    {
        if (interectsWithLeftX(*this, obj)) {
            reflectToQuadrantOneIfIntersectsWithY(obj);
        }
        else if (interectsWithBottomY(*this, obj)) {
            reflectToQuadrantThreeIfIntersectsWithX(obj);
        }
    }

    void GameObject::reflectFromQuadrantThreeIfHit(const GameObject& obj)
    {
        if (interectsWithLeftX(*this, obj)) {
            reflectToQuadrantFourIfIntersectsWithY(obj);
        }
        else if (interectsWithTopY(*this, obj)) {
            reflectToQuadrantTwoIfIntersectsWithX(obj);
        }
    }

    void GameObject::reflectFromQuadrantFourIfHit(const GameObject& obj)
    {
        if (interectsWithRightX(*this, obj)) {
            reflectToQuadrantThreeIfIntersectsWithY(obj);
        }
        else if (interectsWithTopY(*this, obj)) {
            reflectToQuadrantOneIfIntersectsWithX(obj);
        }
    }

    void GameObject::reflectToQuadrantFourIfIntersectsWithX(
            const GameObject& obj)
    {
        if (isInsideWithX(*this, obj)) {
            toQuadrantFour();
        }
        else if (intersectsFromRigthWithX(*this, obj) ||
                 intersectsFromLeftWithX(*this, obj)) {
            toQuadrantFour();
            mQuadrantAngle = increaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithBottomY(*this, obj);
    }

    void GameObject::reflectToQuadrantTwoIfIntersectsWithY(
            const GameObject& obj)
    {
        if (isInsideWithY(*this, obj)) {
            toQuadrantTwo();
        }
        else if (intersectsFromTopWithY(*this, obj) ||
                 intersectsFromBottomWithY(*this, obj)) {
            toQuadrantTwo();
            mQuadrantAngle = increaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithRightX(*this, obj);
    }

    void GameObject::reflectToQuadrantThreeIfIntersectsWithX(
            const GameObject& obj)
    {
        if (isInsideWithX(*this, obj)) {
            toQuadrantThree();
        }
        else if (intersectsFromRigthWithX(*this, obj) ||
                 intersectsFromLeftWithX(*this, obj)) {
            toQuadrantThree();
            mQuadrantAngle = decreaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithBottomY(*this, obj);
    }

    void GameObject::reflectToQuadrantOneIfIntersectsWithY(
            const GameObject& obj)
    {
        if (isInsideWithY(*this, obj)) {
            toQuadrantOne();
        }
        else if (intersectsFromTopWithY(*this, obj) ||
                 intersectsFromBottomWithY(*this, obj)) {
            toQuadrantOne();
            mQuadrantAngle = decreaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithLeftX(*this, obj);
    }

    void GameObject::reflectToQuadrantTwoIfIntersectsWithX(
            const GameObject& obj)
    {
        if (isInsideWithX(*this, obj)) {
            toQuadrantTwo();
        }
        else if (intersectsFromRigthWithX(*this, obj) ||
                 intersectsFromLeftWithX(*this, obj)) {
            toQuadrantTwo();
            mQuadrantAngle = increaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithTopY(*this, obj);
    }

    void GameObject::reflectToQuadrantFourIfIntersectsWithY(
            const GameObject& obj)
    {
        if (isInsideWithY(*this, obj)) {
            toQuadrantFour();
        }
        else if (intersectsFromTopWithY(*this, obj) ||
                 intersectsFromBottomWithY(*this, obj)) {
            toQuadrantFour();
            mQuadrantAngle = increaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithLeftX(*this, obj);
    }

    void GameObject::reflectToQuadrantOneIfIntersectsWithX(
            const GameObject& obj)
    {
        if (isInsideWithX(*this, obj)) {
            toQuadrantOne();
        }
        else if (intersectsFromRigthWithX(*this, obj) ||
                 intersectsFromLeftWithX(*this, obj)) {
            toQuadrantOne();
            mQuadrantAngle = decreaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithTopY(*this, obj);
    }

    void GameObject::reflectToQuadrantThreeIfIntersectsWithY(
            const GameObject& obj)
    {
        if (isInsideWithY(*this, obj)) {
            toQuadrantThree();
        }
        else if (intersectsFromTopWithY(*this, obj) ||
                 intersectsFromBottomWithY(*this, obj)) {
            toQuadrantThree();
            mQuadrantAngle = decreaseAngle(mQuadrantAngle);
        }
        else {
            return;
        }
        putBeforeIntersectsWithRightX(*this, obj);
    }

    void GameObject::toQuadrantOne()
    {
        mQuadrant = Quadrant::I;
        mQuadrantAngle = mirror(mQuadrantAngle);
    }

    void GameObject::toQuadrantTwo()
    {
        mQuadrant = Quadrant::II;
        mQuadrantAngle = mirror(mQuadrantAngle);
    }

    void GameObject::toQuadrantThree()
    {
        mQuadrant = Quadrant::III;
        mQuadrantAngle = mirror(mQuadrantAngle);
    }

    void GameObject::toQuadrantFour()
    {
        mQuadrant = Quadrant::IV;
        mQuadrantAngle = mirror(mQuadrantAngle);
    }

    bool isInQuadrantOne(double angle)
    {
        return angle >= deg_0 && angle <= deg_90;
    }

    bool isInQuadrantTwo(double angle)
    {
        return angle > deg_90 && angle <= deg_180;
    }

    bool isInQuadrantThree(double angle)
    {
        return angle > deg_180 && angle <= deg_270;
    }

    bool isInQuadrantFour(double angle)
    {
        return angle > deg_270 && angle <= deg_360;
    }

    bool interectsWithRightX(const GameObject& a, const GameObject& b)
    {
        return a.bottomRight().x >= b.topLeft().x &&
               a.topLeft().x < b.topLeft().x;
    }

    void putBeforeIntersectsWithRightX(GameObject& a, const GameObject& b)
    {
        Point p = a.topLeft();
        p.x = b.topLeft().x - a.width();
        a.setTopLeft(p);
    }

    bool interectsWithLeftX(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().x <= b.bottomRight().x &&
               a.bottomRight().x > b.bottomRight().x;
    }

    void putBeforeIntersectsWithLeftX(GameObject& a, const GameObject& b)
    {
        Point p = a.topLeft();
        p.x = b.bottomRight().x;
        a.setTopLeft(p);
    }

    bool interectsWithBottomY(const GameObject& a, const GameObject& b)
    {
        return a.bottomRight().y >= b.topLeft().y &&
               a.topLeft().y < b.topLeft().y;
    }

    void putBeforeIntersectsWithBottomY(GameObject& a, const GameObject& b)
    {
        Point p = a.topLeft();
        p.y = b.topLeft().y - a.height();
        a.setTopLeft(p);
    }

    bool interectsWithTopY(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().y <= b.bottomRight().y &&
               a.bottomRight().y > b.bottomRight().y;
    }

    void putBeforeIntersectsWithTopY(GameObject& a, const GameObject& b)
    {
        Point p = a.topLeft();
        p.y = b.bottomRight().y;
        a.setTopLeft(p);
    }

    bool isInsideWithY(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().y >= b.topLeft().y &&
               a.bottomRight().y <= b.bottomRight().y;
    }

    bool isInsideWithX(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().x >= b.topLeft().x &&
               a.bottomRight().x <= b.bottomRight().x;
    }

    bool intersectsFromRigthWithX(const GameObject& a, const GameObject& b)
    {
        return a.bottomRight().x >= b.topLeft().x &&
               a.bottomRight().x <= b.bottomRight().x &&
               a.topLeft().x < b.topLeft().x;
    }

    bool intersectsFromLeftWithX(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().x >= b.topLeft().x &&
               a.topLeft().x <= b.bottomRight().x &&
               a.bottomRight().x > b.bottomRight().x;
    }

    bool intersectsFromTopWithY(const GameObject& a, const GameObject& b)
    {
        return a.bottomRight().y >= b.topLeft().y &&
               a.bottomRight().y <= b.bottomRight().y &&
               a.topLeft().y < b.topLeft().y;
    }

    bool intersectsFromBottomWithY(const GameObject& a, const GameObject& b)
    {
        return a.topLeft().y >= b.topLeft().y &&
               a.topLeft().y <= b.bottomRight().y &&
               a.bottomRight().y > b.bottomRight().y;
    }

    Point calcDelta(double quadrantAngle, Quadrant quadrant, double sideC)
    {
        if (nearlyEqual(sideC, 0.0)) {
            return Point{ 0,0 };
        }

        auto sideA = sin(quadrantAngle) * sideC;
        auto sideB = cos(quadrantAngle) * sideC;

        Point ret;
        switch (quadrant)
        {
            case Quadrant::I:
                ret.x = sideB;
                ret.y = sideA;
                break;
            case Quadrant::II:
                ret.x = -sideA;
                ret.y = sideB;
                break;
            case Quadrant::III:
                ret.x = -sideB;
                ret.y = -sideA;
                break;
            case Quadrant::IV:
                ret.x = sideA;
                ret.y = -sideB;
                break;
        }
        return ret;
    }

    double calcTraveldWay(double deltaTimeMS, double velocityInS)
    {
        return deltaTimeMS / 1000.0 * velocityInS;
    }

    double calcAlphaIfOver360(double alpha)
    {
        if (alpha > deg_360) {
            alpha -= deg_360;
        }
        return alpha;
    }

    Quadrant calcQuadrant(double alpha)
    {
        if (isInQuadrantOne(alpha)) {
            return Quadrant::I;
        }
        if (isInQuadrantTwo(alpha)) {
            return Quadrant::II;
        }
        if (isInQuadrantThree(alpha)) {
            return Quadrant::III;
        }
        return Quadrant::IV;
    }

    double angleToQuadrantAngle(double angle, Quadrant quadrant)
    {
        return angle - deg_90 * static_cast<int>(quadrant);
    }

    double qudrantAngleToAngle(double quadrantAngle, Quadrant quadrant)
    {
        return quadrantAngle + deg_90 * static_cast<int>(quadrant);
    }

    double increaseAngle(double quadrantAngle)
    {
        quadrantAngle *= 1.03;
        return std::clamp(quadrantAngle, 0.0, deg_60);
    }

    double decreaseAngle(double quadrantAngle)
    {
        return quadrantAngle * 0.97;
    }

    double mirror(double quadrantAngle)
    {
        return deg_90 - quadrantAngle;
    }

}  // namespace arkanoid